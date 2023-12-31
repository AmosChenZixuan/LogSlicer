from .base_preprocessor import BasePreprocessor

from utils.dlt.data_types import NestedDefaultdict, DLTPayload
from utils.dlt.text_splitters import DLTBlockSplitter
from utils.templates import SessionBlockTemplate, SessionLineTemplate
from loaders import DLTLoader

class DLTPreprocessor(BasePreprocessor):
    def extract_documents(self, filename):
        d = DLTLoader(filename)
        msgs = d.msgs

        dlt_store = self.create_dlt_store(msgs)

        
        total = 0
        counts = []
        documents = []
        for ecu_name, ecu in dlt_store.items():
            for app_name, app in ecu.items():
                for ctx_name, ctx in app.items():
                    for ses_name, session in ctx.items():
                        counts.append(len(session))
                        block_name = f"{ecu_name}-{app_name}-{ctx_name}-{ses_name}"

                        lines = []
                        for payload, count in session.items():
                            total += count
                            lines.append(SessionLineTemplate().format(index=payload.dlt_index,
                                                                    count=count,
                                                                    type=payload.msg_type,
                                                                    payload=payload))
                            
                        documents.append(SessionBlockTemplate().format(title=block_name,
                                                                    content='\n'.join(lines)))
        # logging.debug(f"Num of Blocks: {len(counts)}")
        # logging.debug(f"Num of Unique Lines: {sum(counts)}")
        # logging.debug(f"Total Num of Lines: {total}")
        return documents

    def chunk_documents(self, documents, chunk_size):
        text_splitter = DLTBlockSplitter(chunk_size)
        chunks = text_splitter.create_documents(['\n'.join(documents)])

        return chunks
    
    @staticmethod
    def create_dlt_store(msgs):
        dlt_store = NestedDefaultdict(int, 5)
        
        for index, m in enumerate(msgs):
            msg_type = m.type_string.decode('utf-8') 
            msg_subtype = m.subtype_string.decode('utf-8')
            if msg_type != 'log' \
                or msg_subtype not in ('!warn', 'error', 'fatal'):  # NOTE: warnings are excluded
                continue 
            
            payload = DLTPayload(m.payload_decoded)\
                        .replace_hex_and_numeric()\
                        .replace_value_before_time_unit()
            
            payload = payload.set_dlt_index(index)\
                            .set_msg_type(msg_subtype)
            
            dlt_store[m.ecuid][m.apid][m.ctid][m.seid][payload] += 1 
            # NOTE: only the first occurence of a payload is stored, so the index will be the first occurence
            # the payload string is stored as the key, no matter of the index or type

        return dlt_store
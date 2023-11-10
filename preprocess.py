import argparse

from utils.data_types import NestedDefaultdict, DLTPayload
from utils.text_splitters import DLTBlockSplitter
from loaders import DLTLoader


parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="Filename to the log file")


def create_dlt_store(msgs):
    print("Creating DLT store...")
    dlt_store = NestedDefaultdict(int, 5)
    
    for m in msgs:
        msg_type = m.type_string.decode('utf-8') 
        msg_subtype = m.subtype_string.decode('utf-8')
        if msg_type != 'log' \
            or msg_subtype not in ('warn', 'error', 'fatal'):
            continue 
        
        payload = DLTPayload(m.payload_decoded)\
                    .replace_hex_and_numeric()\
                    .replace_value_before_time_unit()
        
        dlt_store[m.ecuid][m.apid][m.ctid][m.seid][(msg_subtype, payload)] += 1 

    return dlt_store

def create_documents():
    print("Creating Documents...")
    args = parser.parse_args()                    
    d = DLTLoader(args.file)
    msgs = d.msgs

    dlt_store = create_dlt_store(msgs)

    
    total = 0
    counts = []
    documents = []
    for ecu_name, ecu in dlt_store.items():
        for app_name, app in ecu.items():
            for ctx_name, ctx in app.items():
                for ses_name, session in ctx.items():
                    counts.append(len(session))
                    block_name = f"{ecu_name} {app_name} {ctx_name} {ses_name}"
                    documents.append(f"START {block_name}")
                    for (mtype, msg), count in session.items():
                        documents.append(f"{count} {mtype}: {msg}")
                        total += count
                    documents.append(f"END")

    print(f"Num of Blocks: {len(counts)}")
    print(f"Num of Unique Lines: {sum(counts)}")
    print(f"Total Num of Lines: {total}")

    return documents

def chunk_documents(documents):
    print("Chunking...")
    text_splitter = DLTBlockSplitter(8000)
    chunks = text_splitter.create_documents(['\n'.join(documents)])

    return chunks


if __name__ == '__main__':

    chunks = chunk_documents(create_documents())
    print(chunks)
    print(f"Num of Chunks: {len(chunks)}")
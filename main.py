import argparse

from loaders import DLTLoader


parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="Filename to the log file")
args = parser.parse_args()                    

d = DLTLoader(args.file)

msgs = d.msgs


print(msgs.counter_total)


def main(msgs, limit=2000):

    extract_payload = lambda msg: msg.payload_decoded
    log = "\n".join(map(extract_payload, msgs[:limit]))


    print(log)

main(msgs)
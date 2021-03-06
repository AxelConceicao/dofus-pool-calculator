import sys
import argparse
from Mage import Mage
from Misc import isModuleExist

def main(args):
    sys.path.append(args.sniffer)
    from Sniffer import Sniffer # pylint: disable=import-error
    sniffer = Sniffer(concatMode=False)
    mage = Mage(sniffer.protocol, args.debug)
    sniffer.run(mage.handle, whitelist=mage.getWhitelist())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sniffer", help="path to the sniffer directory", type=isModuleExist)
    parser.add_argument("-d", "--debug", help="show debug logs", action='store_true')
    main(parser.parse_args())
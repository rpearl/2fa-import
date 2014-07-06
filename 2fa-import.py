import argparse
import sqlite3
import sys
import urllib
import qrcode

def main():
    parser = argparse.ArgumentParser(description=
                                     'Generate QR codes for every 2FA code in a'
                                     'Google Authenticator database')
    parser.add_argument('file', help='Path to sqlite3 database', type=str)
    args = parser.parse_args()
    conn = sqlite3.connect(args.file)

    for row in conn.execute('select * from accounts'):
        _id, email, secret, counter, typ, provider, issuer, original_name = row
        keytype = 'totp' if typ == 0 else 'hotp'
        queryargs = dict(secret=secret)
        if issuer:
            queryargs['issuer'] = issuer
        url = 'otpauth://%s/%s?%s' % (keytype, urllib.quote(email), urllib.urlencode(queryargs))

        qr = qrcode.QRCode()
        qr.add_data(url)
        sys.stdout.write("\x1b[2J\x1b[H")
        qr.print_tty()
        try:
            raw_input()
        except KeyboardInterrupt:
            print "Stopping early."
            return
    sys.stdout.write("\x1b[2J\x1b[H")
if __name__ == '__main__':
    main()

import smtplib
carriers = {
    'att':    '@txt.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}
#703-832-6846
"dd5095a2ee88296b348584cdc368ff3a-0f1db83d-e4fadb2e"
def send(message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = '7036290239{}'.format(carriers['verizon'])
    auth = ('testmctestface08@gmail.com', 'airvubcvquirylvq')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)
    

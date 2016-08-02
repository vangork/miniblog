def generate_mail_body(content):
    template = '<html xmlns:v=3D"urn:schemas-microsoft-com:vml" xmlns:o=3D"urn:schemas-microsoft-com:office:office" xmlns:w=3D"urn:schemas-microsoft-com:office:word" xmlns:m=3D"http://schemas.microsoft.com/office/2004/12/omml" xmlns=3D"http://www.w3.org/TR/REC-html40"><head><meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Dutf-8"><meta name=3D"Generator" content=3D"Microsoft Word 15 (filtered medium)"></head><body lang=3D"EN-US" link=3D"#0563C1" vlink=3D"#954F72"><div class=3D"WordSection1">'
    for line in content:
        if line:
            template += '<p class=3D"MsoNormal">' + line + '<o:p></o:p></p>'
        else:
            template += '<p class=3D"MsoNormal"><o:p>&nbsp;</o:p></p>'
    template += '<p class=3D"MsoNormal"><o:p>&nbsp;</o:p></p><p class=3D"MsoNormal">Cheers,<o:p></o:p></p><p class=3D"MsoNormal">miniblog <o:p></o:p></p><p class=3D"MsoNormal"><o:p>&nbsp;</o:p></p></div></body></html>'
    return template
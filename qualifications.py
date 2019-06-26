import re
from bs4 import BeautifulSoup
from methods import get_qual_link, rework
import requests

def get_qual(credentials, period):
    # Entering to cursos section
    headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "intrawww.ing.puc.cl",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

    url = "https://intrawww.ing.puc.cl/siding/index.phtml"
    s = requests.Session()
    login_response = s.post(url, data=credentials, headers=headers, allow_redirects=True)
    entering = True

    if "incorrectos" in login_response.text:
        entering = False
        html_string = ""
        name_button = "Datos incorrectos, vuelve a ingresarlos"

    else:
        ck = s.cookies.get_dict()
        url = "https://intrawww.ing.puc.cl" + period
        response = s.get(url, data=credentials, headers=headers, cookies=ck)

        print(response.text)
        
        html_string = ""
        name_button = "Back"
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for atag in soup.find_all('a', href=True):
            if "accion_curso" in atag["href"]:
                links.append(get_qual_link(atag["href"]))

        for link in links:
            qual = "https://intrawww.ing.puc.cl/siding/dirdes/ingcursos/cursos/index.phtml?accion_curso=notas&acc_notas=mostrar_notas&"+link+"&solo_vista=1"
            response = s.get(qual, data=credentials, headers=headers, cookies=ck)
            while "500 Internal Server Error" in response.text:
                response = s.get(qual, data=credentials, headers=headers, cookies=ck)
            qual_soup = BeautifulSoup(response.text, "html.parser")
            curso = ""
            for b_tag in qual_soup.find_all("td", class_=True):
                if "ColorFondoResaltado" in b_tag["class"]:
                        if "|" in str(b_tag):
                                curso = str(b_tag)

            for table in qual_soup.find_all("table", style=True):
                if "back" in table["style"]:
                        html_string += rework(curso + "\n" + str(table))

    s.close()

    string = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Notas SIDING</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    <!--===============================================================================================-->
        <link rel="icon" type="image/png" href="{{ url_for('static', filename='table/images/icons/favicon.ico') }}"/>
    <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='table/vendor/bootstrap/css/bootstrap.min.css') }}">
    <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='table/fonts/font-awesome-4.7.0/css/font-awesome.min.css') }}">
    <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='table/vendor/animate/animate.css') }}">
    <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='table/vendor/select2/select2.min.css') }}">
    <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='table/vendor/perfect-scrollbar/perfect-scrollbar.css"') }}">
    <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='table/css/util.css') }}">
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='table/css/main.css') }}">
    <!--===============================================================================================-->
    </head>
    <body>
        <form action = "/" class="contact100-form validate-form">
            <div class="container-contact100-form-btn">
                <button class="contact100-form-btn">
                    <span>
                        <i class="fa fa-paper-plane-o m-r-6" aria-hidden="true"></i>"""+ name_button + """
                    </span>
                </button>
            </div>
        </form>
        """ + html_string +"""

    

    <!--===============================================================================================-->
        <script src="{{ url_for('static', filename='table/vendor/jquery/jquery-3.2.1.min.js') }}"></script>
    <!--===============================================================================================-->
        <script src="{{ url_for('static', filename='table/vendor/bootstrap/js/popper.js') }}"></script>
        <script src="{{ url_for('static', filename='table/vendor/bootstrap/js/bootstrap.min.js') }}"></script>
    <!--===============================================================================================-->
        <script src="{{ url_for('static', filename='table/vendor/select2/select2.min.js') }}"></script>
    <!--===============================================================================================-->
        <script src="{{ url_for('static', filename='table/js/main.js') }}"></script>

    </body>
    </html>

    """

    return string

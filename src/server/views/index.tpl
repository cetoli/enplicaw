<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><!--

############################################################
Super Python - User Programming Interface
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2015/04/06
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2015, `GPL <http://is.gd/3Udt>`__.
-->
<html>
<head>
    <meta charset="iso-8859-1" />
    <title>Enplicaw</title>
    <meta http-equiv="content-type" content="application/x-www-form-urlencoded;charset=utf-8" />
    <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon" />
    <link rel="stylesheet" href="style.css" type="text/css" />
        <style>
            body, html {
                margin: 0;
                height: 100%;
                width: 100%;
            }

            #tit {
                background-color: ivory;
                background-position: center;
                background-repeat: no-repeat;
                margin: 0 auto;
                display: table;
                text-align: center;
                padding: 10px;
            }
            #menu {
                background-color: ivory;
                background-position: center;
                background-repeat: no-repeat;
                max-height: 80%;
                max-width: 90%;
                height: 100%;
                width: 100%;
                margin: 0 auto;
                display: table;
                text-align: center;
                padding: 10px;
            }
            .item {
                height: 120px;
                width: 130px;
                margin: 5px;
                display: inline-block;
            }
            .stretch {
                width: 100%;
                display: inline-block;
                font-size: 0;
                line-height: 0
            }


        </style>

</head>
<body>
    <h1 id="tit"> {{ title }}</h1>
    <form action="main/identify" method="post">
        <div id="menu">
            <div id="banner"><img src="{{ image }}" height="300"/></div>
            % for item in identification:
                <div class="item">
                    <span>{{ item["label"] }}:</span><br/>
                    <input type="text" name="{{ item['name'] }}"/>
                </div>
            %end
        <div id="submit" class="item">
                    <input type="submit" value="{{ submit }}"/>
        </div>

        </div>
    </form>
</body>
</html>

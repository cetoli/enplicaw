<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Resultado do Superpython</title>
    <link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
    <h1>Resultado da Enquete Superpython</h1>
    <table id="box-table-a" >

        <thead>
            <tr>
                <th scope="col"><span>Questão</span></th>
                % for item in columns:

                    <th scope="col"><span>{{ item }}</span></th>

                % end

            </tr>
        </thead>


        <tbody>
            % for line in result:
            <tr>
                <td><span>{{ line.label }}</span></td>
                % for item in line.value:

                    <td scope="col"><span>{{ item }}</span></td>

                % end
           </tr>
            % end
        </tbody>

    </table>
{{ data }}
</body>
</html>

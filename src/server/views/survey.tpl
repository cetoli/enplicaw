<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Enquete : {{ title }}</title>
    <link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
    <h1>Enquete do projeto {{ title }}</h1>
    <form action="survey" method="post">
        <span></span>

    <table id="box-table-a" style="width: 800px;">

        <thead>
            <tr>
                <th scope="col"><span>ITEM</span></th>

                <th scope="col" colspan="{{ columns }}"><span>PERGUNTA</span></th>

            </tr>
        </thead>


        <tbody>
            <tr>
                <td colspan="2"><span>Nome do Estudante:</span></td>
                <td colspan="{{ columns - 1}}"><span><input type="text" name="name" size="60"></input></span></td>
           </tr>
            % for question in survey:
            <tr>
                <td><span>{{ question.name }}</span></td>
                <td colspan="{{ columns }}"><span>{{ question.label }}</span></td>
           </tr>
            <tr>
                <td><span></span></td>
                % for answer in question.value:
                <td><span><input type="radio" name="{{ question.name }}" value="{{ answer }}">{{ answer }}</input></span></td>
                % end
            </tr>
            % end
            <tr>
                <td colspan="{{ columns + 1}}"><span><input type="submit" name="submit" size="60" value="      Enviar Dados      "></input></span></td>
            </tr>
        </tbody>

    </table>
</form>
</body>
</html>

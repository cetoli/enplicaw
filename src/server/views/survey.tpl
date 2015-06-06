<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="application/x-www-form-urlencoded;charset=UTF-8"/>
    <title>Enquete : {{ title }}</title>
    <link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
    <h1>Enquete do projeto {{ title }}</h1>
    <form action="survey" method="post">
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
                <td colspan="{{ columns - 4}}">
                    <input type="text" name="name" size="40"></input>
                </td>
                <td colspan="3"><span>Superdotado:</span>
                    <input type="radio" name="super" value="s">Sim</input>
                    <input type="radio" name="super" value="n" checked>Não</input>
                </td>
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
                <td colspan="{{ columns//2 + 1}}"><span><input type="submit" name="submit" size="60" value="      Enviar Dados e Entrar Novo Aluno      "></input></span></td>
                <td colspan="{{ columns - columns//2}}"><span><input type="submit" name="lastsubmit"  onclick='this.form.action="endsurvey";' value="      Enviar Dados e Terminar      "></input></span></td>
            </tr>
        </tbody>

    </table>
</form>
</body>
</html>

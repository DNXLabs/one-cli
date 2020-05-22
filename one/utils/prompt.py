from PyInquirer import style_from_dict, Token


style = style_from_dict({
    Token.Separator: '#50A8E2',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#50A8E2',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

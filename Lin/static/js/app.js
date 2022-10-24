function valueColor() { 
    rate = document.getElementById('rate').innerText
    rate = parseFloat(rate)
    element = document.getElementById("color");
    if (eval(rate) === eval(0))
        {element.style.color = '#6c6c6c';}
    else if (eval(rate) <eval(5))  
        {element.style.color = '#79ff79';}
    else if (eval(rate) <eval(10))  
        {element.style.color = '#00db00';}   
    else if (eval(rate) < eval(15))  
        {element.style.color = '#009100';}
    else if (eval(rate) < eval(20) ) 
        {element.style.color = '#006000';}
    else if (eval(rate) >= eval(-5)) 
        {element.style.color = '#ff2d2d';}
    else if (eval(rate) > eval(-10)) 
        {element.style.color = '#ea0000';}    
    else if (eval(rate) >eval( -15)) 
        {element.style.color = '#ae0000';}
    else if(eval(rate) > eval(-21))  
        {element.style.color = '#6c6c6c';} 
}

valueColor();
/**
 * Utiliza un event stream para obtener el estado de 
 * la planta y si se le pasa, tambiene ejecura una funcion 
 * al recibir un mensaje
 */
function state_handler(custom_function){
  var source = new EventSource('/stream');
  source.onmessage = function(event){
    window.state = JSON.parse(event.data);
    if (typeof custom_function === 'function'){
      custom_function(window.state);
    };
  };
};
function update_tag(name, value, postfix){
    var postfix = postfix || '';
    if (Math.round(value) !== value){
      value = value.toFixed(2);
    };
    $("#" + name).text(value + " " + postfix);
};
/**
 * Actualiza una barra de progreso de bootstrap
 */
function update_bar(name, value, postfix, max){
    var max = max || 100;
    var percent = (value / max ) * 100;
    if (percent > 100){
      percent = 100;
    };
    $("#" + name).css('width', percent + "%");
    update_tag(name, value, postfix);
    update_tag(name + "_val", value, postfix);
};

function _crear_div_alarma(text, time){
  var div = document.createElement('div');
  var boton = document.createElement('button');
  boton.type = 'button';
  boton.setAttribute('data-dismiss', 'alert');
  boton.classList.add('close');
  boton.innerHTML = '&times;';
  div.classList.add('alert');
  div.appendChild(boton);
  timestamp = document.createElement('strong');
  timestamp.innerText = time;
  div.appendChild(timestamp); 
  div.innerHTML += " " + text;
 
  return div;
};

function set_alert(text, time){
  var container = $('#alert_container');
  var div = _crear_div_alarma(text, time); 
  container.prepend(div);
};


function set_notify(text, time){
  var container = $('#event_container');
  var div = _crear_div_alarma(text, time); 
  div.classList.add('alert-success');
  container.prepend(div);
};

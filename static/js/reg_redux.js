let styleChangePassword = () => {
  let label;
  let input;
  let labelClasses = ['form-control-label', 'col-sm-3', 'text-right', 'pt5'];
  let inputClasses = ['textinput', 'textInput', 'form-control'];
  let fieldWrapperDivs = document.querySelectorAll('div.fieldWrapper');
  fieldWrapperDivs.forEach(div => {
    label = div.children[0];
    input = div.children[1].children[0];
    if (input.required) {
      labelClasses.push('requiredField');
      label.innerText += ' *';
    }
    label.classList.add(...labelClasses);
    input.classList.add(...inputClasses);
    if (div.children[3]) {
      div.children[3].classList.add('offset-sm-3', 'password-help', 'text-muted');
    }
  });
};

let styleLogin = () => {
  document.querySelector('body').classList.add('gray-bg')
  let label;
  let input;
  let labelClasses = ['sr-only'];
  let inputClasses = ['textinput', 'textInput', 'form-control'];
  let fieldWrapperDivs = document.querySelectorAll('div.fieldWrapper');
  fieldWrapperDivs.forEach(div => {
    label = div.children[0];
    input = div.children[1];
    label.classList.add(...labelClasses);
    input.classList.add(...inputClasses);
    input.setAttribute('placeholder', label.innerText.replace(':', ''));
  });
};

let checkTitle = () => {
  let title = document.title;
  if (title.indexOf('Login') >= 0) {
    styleLogin();
  } else if (title.indexOf('Change Password') >= 0) {
    styleChangePassword();
  }
};

checkTitle();

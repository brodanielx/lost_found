
let makeFormGroupsInline = () => {
  let formGroups = document.querySelectorAll('.form-group');
  formGroups.forEach(group => {
    group.classList.add('row');
  });
};

makeFormGroupsInline();

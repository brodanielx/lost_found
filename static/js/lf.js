
let makeFormGroupsInline = () => {
  let formGroups = document.querySelectorAll('.form-group');
  formGroups.forEach(group => {
    group.classList.add('row');
  });
};

makeFormGroupsInline();


// let navs = document.querySelectorAll('.nav-item')
// let removeActive = () => {
//   navs.forEach(nav => {
//     if (nav.classList.contains('active')) {
//       nav.classList.remove('active')
//     }
//   })
// }
//
// let navBarClick = (nav) => {
//   removeActive();
//   nav.classList.add('active')
// }
//
// navs.forEach(nav => {
//   nav.addEventListener("click", () => {
//     navBarClick(nav)
//   });
// })

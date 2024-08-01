const productName = document.querySelectorAll(".productName");
const navBarLinks = document.querySelector("#navBarLinks");
const hiddenContent = document.querySelector("#hiddenContent");
const hiddenScrollDiv = document.querySelector("#hiddenScrollDiv");
const sortsProductsLinkCont = document.querySelectorAll(
  "#sortsProductsLinkCont a"
);
const producsUl = document.querySelectorAll("#producsUlParent ul");
const accountSetting = document.querySelector("#accountSetting");
const accountSettingCont = document.querySelector("#accountSettingCont");
const mainMenuNavBarClickElement = document.querySelectorAll(
  ".mainMenuNavBarClickElement"
);
const mainMenuNavBarClickElementUls = document.querySelectorAll(
  ".mainMenuNavBarClickElement + ul"
);
const closeMainMenuNavBar = document.querySelector("#closeMainMenuNavBar");
const mainMenuNavBarsec = document.querySelector("#mainMenuNavBarsec");
const openMainMenuNavBar = document.querySelector("#openMainMenuNavBar");
const scrollTop = document.querySelector("#scrollTop");

let oldScrollY = scrollY;
let istouch = true;
productName.forEach((input) => {
  input.addEventListener("focus", () => {
    hiddenContent.classList.add("show");
    document.body.classList.add("overflow-hidden");
    input.parentElement.classList.add("headerFormFoucsStyle");
    input.id = "search";
    location.hash = input.id;
  });
  input.addEventListener("blur", () => {
    hiddenContent.classList.remove("show");
    document.body.classList.remove("overflow-hidden");
    input.parentElement.classList.remove("headerFormFoucsStyle");
    input.id = "";
    location.hash = "";
  });
});

navBarLinks.addEventListener("mouseover", () => {
  productName.forEach((input) => {
    input.blur();
  });
  hiddenContent.classList.add("show");
  document.body.classList.add("overflow-hidden");
});
navBarLinks.addEventListener("mouseleave", () => {
  hiddenContent.classList.remove("show");
  document.body.classList.remove("overflow-hidden");
});

window.addEventListener("scroll", () => {
  if (oldScrollY > scrollY) {
    oldScrollY = scrollY;
    hiddenScrollDiv.parentElement.classList.remove("hideWithTranslateY");
  } else if (oldScrollY <= scrollY) {
    oldScrollY = scrollY;
    hiddenScrollDiv.parentElement.classList.add("hideWithTranslateY");
  }
});

Array.from(sortsProductsLinkCont).forEach((link, index) => {
  link.addEventListener("mouseover", () => {
    Array.from(sortsProductsLinkCont).forEach((item, ind) => {
      producsUl[ind].classList.remove("flexShow");
      item.classList.remove("headerNavHoverStyle");
    });
    link.classList.add("headerNavHoverStyle");
    producsUl.forEach((ul) => {
      if (link.value === producsUl[index].value)
        producsUl[index].classList.add("flexShow");
    });
  });
});
window.addEventListener("click", (e) => {
  if (
    e.target !== accountSetting &&
    e.target !== accountSetting.children[0] &&
    e.target !== accountSetting.children[1]
  )
    accountSettingCont.classList.remove("show");
});
accountSetting.addEventListener("click", () => {
  accountSettingCont.classList.toggle("show");

  istouch = true;
});
mainMenuNavBarClickElement.forEach((btn, index) => {
  btn.addEventListener("click", () => {
    mainMenuNavBarClickElementUls[index].classList.toggle("showUl");
    btn.classList.toggle("showed");
  });
});

openMainMenuNavBar.addEventListener("click", () => {
  mainMenuNavBarsec.classList.remove("hidden");
  mainMenuNavBarsec.classList.add("setDisplay");
  mainMenuNavBarsec.classList.add("active");
});

mainMenuNavBarsec.addEventListener("click", (e) => {
  console.log(e.target);
  if (e.target !== mainMenuNavBarsec && e.target !== openMainMenuNavBar) return;
  mainMenuNavBarsec.classList.remove("active");
});

mainMenuNavBarsec.onanimationend = () => {
  if (!mainMenuNavBarsec.classList.contains("active"))
    mainMenuNavBarsec.classList.remove("setDisplay");
};

closeMainMenuNavBar.addEventListener("click", () => mainMenuNavBarsec.click());

scrollTop.addEventListener("click", () => {
  scrollTo(0, 0);
});

window.addEventListener("scroll", () => {
  if (scrollY > 100) scrollTop.classList.add("active");
  else scrollTop.classList.remove("active");
});

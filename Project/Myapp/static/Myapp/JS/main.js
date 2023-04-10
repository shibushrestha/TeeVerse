/* Open the sidenav */
function openNav() {
    document.getElementById("mySidenav").style.cssText = `transition:0.5s; width:100%`
}

/* Set the width of the side navigation to 0 */
function closeNav(){
    document.getElementById("mySidenav").style.cssText = `transition: 0.3s; width:0`
} 

const profileBtn = document.querySelector(".profile");
profileBtn.addEventListener('click', ()=>{
    profileTab();
});

const profileTab = (function(){
    let clickStatus = false;
    const profileCard = document.querySelector(".profile-card");
    return function(){
        if(clickStatus === false){
            profileBtn.style.backgroundColor = "rgba(28, 172, 139, 0.8)";
            profileCard.style.display = "flex";
            clickStatus = true;     
        }else{
            profileBtn.style.backgroundColor = "white";
            profileCard.style.display = "none";
            clickStatus = false;
        }
    };
})();

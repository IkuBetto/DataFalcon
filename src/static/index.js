function chbg(chkID){
    Myid = document.getElementById(chkID);
    Mylabel = document.getElementById(chkID+'label');
    Cbox = document.getElementsByClassName("datecheck");
    Myborder = document.getElementsByClassName("date_border");
    Myplace = document.getElementById(chkID + 'place');
    Cplace = document.getElementsByClassName("raceplacebutton");
    Mytable = document.getElementsByClassName("race-table");
    Date_place = document.getElementsByClassName("date_place");
    ps = document.getElementsByClassName("place_str");
    for(i=0;i<Date_place.length;i++){
        Date_place[i].checked = 'false';
        ps[i].style.color='rgb(49,104,87)';
        ps[i].style.backgroundColor='white';
    }
    for(i=0;i<Cbox.length;i++){
        if(Cbox[i].checked){
            Myborder[i].style.fontWeight = 'bold';
            Myborder[i].style.color = 'rgb(49,104,87)';
            Myborder[i].style.borderBottom = '3px solid rgb(49,104,87)';
            Myplace.style.display = 'block';
        }else{
            Myborder[i].style.fontWeight = 'normal';
            Myborder[i].style.color = 'rgb(191,191,191)';
            Myborder[i].style.borderBottom = '1px solid rgb(191,191,191)';
            Cplace[i].style.display = 'none';
        }
    }
    for(i=0;i<Mytable.length;i++){
        Mytable[i].style.display = 'none';
    }

}

function chtable(dayID, placeID){
    Placeid = document.getElementById(dayID+placeID);
    Tableid = document.getElementById(dayID+placeID+'table');
    Tableclass = document.getElementsByClassName("race-table");
    Placeclass = document.getElementsByClassName("date_place");
    Mylabel = document.getElementById(dayID+placeID+'label');
    ps = document.getElementsByClassName("place_str");
    for(i=0;i<Tableclass.length;i++){
        Tableclass[i].style.display = 'none';
    }
    for(i=0;i<Placeclass.length;i++){
        if(Placeclass[i].checked){
            ps[i].style.color='white';
            ps[i].style.backgroundColor='rgb(49,104,87)';
            Tableid.style.display='table';
        }else{
            ps[i].style.color='rgb(49,104,87)';
            ps[i].style.backgroundColor='white';
        }
    }
}

function emerge(){
    id = document.getElementById("search_form");
    id.style.display = "block";
}

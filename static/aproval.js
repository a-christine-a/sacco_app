



let id = "";
function aproval(myVal)
{
    // console.log("checked: ", document.getElementById("_" + myVal).value);
    if(confirm("Are you sure you wanna select: " + myVal + ", once selected can only be unselected by Reset Button") == 1)
    {
        alert('Successfully selected');
        id += (myVal + " ");
        document.getElementById("selected").value = id;
    }
    else{
        alert("Selection cancelled!!")
    }    
    // alert(id);

}

let d_id = "";
function disbustal(myVal1)
{
    if(confirm("Are you sure you wanna select: " + myVal1 + ", once selected can only be unselected by Reset Button") == 1)
    {
        alert('Disbust Successfully selected');
        d_id += (myVal1 + " ");
        document.getElementById("d_select").value = d_id;
    }
    else{
        alert("Selection cancelled!!");
    }
}
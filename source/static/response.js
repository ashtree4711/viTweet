/**
 * Created by Lara on 26.02.19.
 */

function loading() {
   $("#loading").show(); //show gif during API request
   $("#content").hide(); //hide jumbotron with text and main search
   $("#uploadOption").hide(); //hide upload option
    
}

//show replies in list visualization
function showReplies() {
    $(".reply").show();
    $("#hidereplynumber").show();
    $("#hidereplynumber2").show();
}

//hide replies in list visualization
function hideReplies() {
    $(".reply").hide();
    $("#hidereplynumber").hide();
    $("#hidereplynumber2").hide();
}

//show quotes in list visualization
function showQuotes() {
    $(".reply").show();
    $("#hidereplynumber").show();
    $("#hidereplynumber2").show();
}

//hide quotes in list visualization
function hideQuotes() {
    $(".reply").hide();
    $("#hidereplynumber").hide();
    $("#hidereplynumber2").hide();
}
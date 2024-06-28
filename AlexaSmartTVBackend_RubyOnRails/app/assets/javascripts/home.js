


$(document).on("click", "#delete_submit", function(event){
     if(!confirm("Are you sure you want to delete this device? This device will appear again if it comes back online.")){
        event.preventDefault();
        return false;
      }
});

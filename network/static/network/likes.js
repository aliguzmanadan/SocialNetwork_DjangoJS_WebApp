document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event => {
        //Get parent of the target of the event
        const element = event.target;

        if (element.id === 'like_button'){

            //Get parent element 
            const post_div = element.parentElement;

            //Get id of the post clicked on
            const post_id = parseInt(element.parentElement.dataset.post_id);
            console.log(post_id);

        }
        
    });
   
    
  });
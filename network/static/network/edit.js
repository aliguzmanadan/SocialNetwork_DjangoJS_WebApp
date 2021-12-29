document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event => {
        //Get parent of the target of the event
        const element = event.target;
        const post_div = element.parentElement;

        //Hide edit button
        post_div.querySelector('#edit_button').style.display = 'none';

        if (element.className === 'btn btn-link'){
            //Get id of the post clicked on
            const post_id = parseInt(post_div.dataset.post_id);
            console.log(post_id);


            //Replace content by form
            const content_div = post_div.querySelector('#content');
            content_div.innerHTML = "";
            const form = document.createElement('form');

            const textarea_space = document.createElement('textarea');
            textarea_space.className = "form-control";
            textarea_space.placeholder = "New post content";
            textarea_space.autofocus = true;

            const save_button = document.createElement('input');
            save_button.className = "btn btn-primary";
            save_button.type = "submit";
            save_button.value = "Save";

            form.append(textarea_space, save_button);
            content_div.append(form);

        
        }
        
    });
   
    
  });
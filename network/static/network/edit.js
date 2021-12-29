document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event => {
        //Get parent of the target of the event
        const element = event.target;

        if (element.className === 'btn btn-link'){

            //Get parent element 
            const post_div = element.parentElement;

            //Hide edit button
            post_div.querySelector('#edit_button').style.display = 'none';

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

            //Handling submissio of form
            form.onsubmit = () => {
                const new_content = textarea_space.value;
                console.log(new_content);

                //Edit post via PUT request to API
                fetch(`/post/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: new_content
                    })
                  })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                })

                //Restore vie of the post
                post_div.querySelector('#edit_button').style.display = 'block';
                content_div.innerHTML = `<p class="card-text" id="post_content"> ${new_content} </p>`;

                //Prevent form from submitting
                return false;
            };

        
        }
        
    });
   
    
  });
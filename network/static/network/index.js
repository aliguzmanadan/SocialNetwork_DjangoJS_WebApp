//import { load_posts,  submit_post} from './functions.js';

document.addEventListener('DOMContentLoaded', function() {

    

    // Use links in the top of the page to toggle between views
    //document.querySelector('#all_posts_link').addEventListener('click', () => load_posts('all'));
    //document.querySelector('#following_link').addEventListener('click', () => load_posts('following'));
    document.querySelector('#post_form').onsubmit =  () => {return submit_post()};

    // By default, load all posts
    //load_posts('all');
   
    
  });

////////////////

function load_posts(posts_set){
    document.querySelector('#session_name').innerHTML = `<h3>${posts_set.charAt(0).toUpperCase() + posts_set.slice(1)}</h3>`;

    //Clearing posts view
    document.querySelector('#session_posts').innerHTML = "";

    //Getting posts
    fetch(`/posts/${posts_set}`)
    .then(response => response.json())
    .then(posts => {
        // Print posts in cosole
        console.log(posts);
        console.log(typeof posts)

        //display each post
        posts.forEach(post => display_post(post));
});
}

////////////////

function display_post(post){

    //Creating div for each post
    let div_post = document.createElement('div');
    div_post.className = "card";

    let body = document.createElement('div');
    body.className = "card-body";
    body.innerHTML = `<h5 class="card-title"> <a href="/user/${post.poster}">${post.poster}</a> </h5>`

    let content = document.createElement('p');
    content.className = "card-text";
    content.innerHTML = post.content;

    let timestamp = document.createElement('p');
    timestamp.className = "card-text";
    timestamp.innerHTML = `<small class="text-muted">${post.timestamp}</small>`;

    let likes = document.createElement('i');
    likes.className = "bi bi-suit-heart-fill";
    likes.innerHTML = `<small class="text-muted" id="likes_number">0</small>`;


    //Assemble post
    body.append(content, timestamp, likes);
    div_post.append(body);
    document.querySelector('#session_posts').append(div_post);


}

//////////////////

function submit_post(){
    
    //Get content of the form
    const content = document.querySelector('#content').value; 
    console.log(content)

    //submit the post via POST request to the API
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });

    //Reload page
    window.location.reload(true);


    //Stop form from submitting
    return false;
}
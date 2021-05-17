document.addEventListener('click', event => {
    
    // Edit post code
    if (event.target.id === "edit" && document.querySelector('#back') === null) {

        // Save previous post info
        const previous = document.querySelector(`#edit_box_${event.target.value}`).innerHTML;
        const previous_id = event.target.value;
        const previous_text = document.querySelector(`#post_text_${event.target.value}`).innerHTML;
        class App extends React.Component  {

            // Create state
            constructor(props) {
                super(props);
                this.state = {
                    text: this.props.previous_text
                };
            }

            // Change text varible in state
            newValueiInsert = (event) => {
                this.setState({
                    text: event.target.value
                });
            }

            // insert new text in db
            Put = () => {   
                fetch(`/post_reduction/${this.props.previous_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        post_id: this.props.previous_id,
                        new_text: this.state.text
                    })
                });
                // Return post with changed text if save clicked
                document.querySelector(`#edit_box_${this.props.previous_id}`).innerHTML = this.props.previous;
                document.querySelector(`#post_text_${this.props.previous_id}`).innerHTML = this.state.text;
            }

            Back = () => {
                
                document.querySelector(`#edit_box_${this.props.previous_id}`).innerHTML = this.props.previous;
            }

            render() {

                // create edit form
                return (
                    <div className="edit_inp">
                        <textarea cols="10" rows="10" className="edit_area" maxLength="255" defaultValue={this.props.previous_text} onChange={this.newValueiInsert}>
                        </textarea>
                        <input type="submit" className="btn btn-primary" onClick={this.Put} id="save_button" value="Save" />
                        <button type="button" className="btn btn-link" onClick={this.Back} id='back'>Back</button>
                    </div>
                );
            };

        }
        ReactDOM.render(<App previous={previous} previous_text={previous_text} previous_id={previous_id} />, document.querySelector(`#edit_box_${previous_id}`));
        
    }


    // Likes
    if (event.target.className === 'hart' && event.target.dataset.is_auth === "True") {
        var action = '';
        if (event.target.dataset.liked === 'false') {
            event.target.src = "/static/network/filled_hart.png";
            event.target.dataset.liked = 'true';
            action = 'add';
        } else {
            event.target.src = "/static/network/empty_hart.png";
            event.target.dataset.liked = 'false';
            action = 'dell';
        }

        fetch('/like', {
            method: 'PUT',
            body: JSON.stringify({
                post_id: event.target.dataset.post_id,
                movement: action
            })
        }).then(response => response.json())
        .then(data => {
            document.querySelector(`#likes_count_${data.post_id}`).innerHTML = data.likes_count;
        });
    }

    // Comments add
    if (event.target.id === "add_comment" && document.querySelector('#back') === null) {

        class NewComment extends React.Component {
            render() {
                return (
                    <div style={{marginTop: '10px'}}>
                        <div style={{fontSize: "smaller"}}>{ this.props.timestamp }</div>
                        <div>From <b>{ this.props.author }</b>: { this.props.text }</div>
                    </div>
                );
            }
        }

        class Comment extends React.Component {
            
            // Create state
            constructor(props) {
                super(props);
                this.state = {
                    text: ''
                };
            }

            // Change text varible in state
            newValueiInsert = (event) => {
                this.setState({
                    text: event.target.value
                });
            }

            Back = () => {
                document.querySelector(".comment_inp").remove();
            }

            newCommentInsert = () => {
                fetch('/comment', {
                    method: 'PUT',
                    body: JSON.stringify({
                        post_id: this.props.post_id,
                        comment_text: this.state.text
                    })
                }).then(response => response.json())
                .then(data => {
                    var next_new_comment_element = document.createElement('div');
                    next_new_comment_element.id = `new_comment_${this.props.post_id}_${data.new_comment_id}`;
                    document.querySelector(`#comments_${event.target.dataset.post_id}`).prepend(next_new_comment_element);
                    ReactDOM.render(<NewComment timestamp={data.timestamp} author={data.author} text={data.text} new_comment_id={data.new_comment_id} />, document.querySelector(`#new_comment_${this.props.post_id}_${data.new_comment_id}`));
                    document.querySelector(`.comment_inp`).remove();
                });
            }

            render() {
                return (
                    <div className="comment_inp">
                        <textarea name="post" cols="40" rows="1" maxLength="255" id="id_post" autoFocus onChange={this.newValueiInsert}>
                        </textarea>
                        <div>
                            <input type="submit" id="comment_button" onClick={this.newCommentInsert} className="comment_buttons" value="Comment" />
                            <input type="submit" id='back' onClick={this.Back} className="comment_buttons" value="Back" />
                        </div>
                    </div>
                );
            }
        }
        
        var new_comment_inp_element = document.createElement('div');
        new_comment_inp_element.id = `inp_${event.target.dataset.post_id}`;
        document.querySelector(`#comments_${event.target.dataset.post_id}`).prepend(new_comment_inp_element);
        ReactDOM.render(<Comment post_id={event.target.dataset.post_id} />, document.querySelector(`#inp_${event.target.dataset.post_id}`));

    }

    return false;
});

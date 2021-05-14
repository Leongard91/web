document.addEventListener('click', event => {
    if (event.target.className === "btn btn-link") {
// !!!!!!!!11111
        class App extends React.Component {
            render() {
                return (
                    <div class="form_area" style="margin-top: 10px;">
                        <form>
                            <textarea name="post" cols="40" rows="10" class="post_form" maxlength="255" id="id_post">
                                document.querySelector() 
                            </textarea>
                            <input type="submit" class="btn btn-primary" id="post_button" value="Save">
                        </form>
                    </div>
                );
            }
        }

        ReactDOM.render(<App />, document.querySelector('.post_area'));
    }
});






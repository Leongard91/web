
document.addEventListener('click', event => {
    if (event.target.innerHTML === 'All Posts') {
        class App extends React.Component {

            render() {
                return <h1>Hello!</h1>
            }
        }
        ReactDOM.render(<App />, document.querySelector('#posts_view'));
        return false;
    }
});





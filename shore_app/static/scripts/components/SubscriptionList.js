import React from 'react';
import { Link } from 'react-router-dom';
import fetchAPI from './Api';

class SubscriptionList extends React.Component {
  // Adapted from - https://reactjs.org/docs/faq-ajax.html
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      user: null,
    };
    this.handleClick = this.handleClick.bind(this);
  }

  async componentDidMount() {

    try {
      const id = this.props.match.params.id;
      const user = await fetchAPI("GET", '/api/user/' + id);

      this.setState({
        user: await user.json()
      });
      const response = await fetchAPI("GET", '/api/subscriptions?user_id=' + this.state.user.id);
      if (response.ok) {
        let data = await response.json();
        this.setState({
          isLoaded: true,
          items: data
        });
      } else {
        return response;
      }
    } catch (error) {
      this.setState({
        isLoaded: true,
        error
      });
    }
  }


  render() {
    const { error, isLoaded, items, user } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <table>
          <tr>
            <td colSpan="4">
              Subscriptions list for <b>{user.name}</b>
            </td>
          </tr>
          <tr>
            <td>Phrases</td><td>Interval (Min)</td><td>Last Email Sent</td><td>Action</td>
          </tr>
          {
            items.map(item => (
              <tr>
                <td>{item.phrases}</td>
                <td>{item.interval}</td>
                <td>{item.last_email_sent}</td>
                <td>
                  <Link to={'/subscription/edit/' + item.id} className="link" activeClassName="active" exact>Edit</Link> |
                <Link value={item.id} onClick={(e) => this.handleClick(e, item.id)}>Delete</Link>
                </td>
              </tr>
            ))
          }
        </table >
      );
    }
  }


  async handleClick(e, id) {
    e.preventDefault();
    const response = await fetchAPI("DELETE", '/api/subscription/' + id);
    if (response.ok) {
      this.state.currentView = <SubscriptionList />
      // window.location.reload(false);
    } else {
      const error = {
        message: response.statusText
      }
      this.setState({
        isLoaded: false,
        error: error
      });
    }
  }

}

export default SubscriptionList;

import React from 'react';
import { Link } from 'react-router-dom';
import fetchAPI from './Api';

class UserList extends React.Component {
  // Adapted from - https://reactjs.org/docs/faq-ajax.html
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
    this.handleClick = this.handleClick.bind(this);
  }

  async componentDidMount() {
    try {
      const response = await fetchAPI("GET", '/api/users');
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
    const { error, isLoaded, items } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <table>
          <tr>
            <td>Name</td><td>Email</td><td>Actions</td>
          </tr>
          {items.map(item => (
            <tr>
              <td>{item.name}</td>
              <td>{item.email}</td>
              <td>
                <Link to={'/edit/' + item.id} className="link" activeClassName="active" exact>Edit</Link> |
                <Link value={item.id} onClick={(e) => this.handleClick(e, item.id)}>Delete</Link>
              </td>
            </tr>
          ))}
        </table>
      );
    }
  }


  async handleClick(e, id) {
    e.preventDefault();
    console.log(id);
    const response = await fetchAPI("DELETE", '/api/user/' + id);
    if (response.ok) {
      window.location.reload();
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

export default UserList;

import React from 'react';
import fetchAPI from './Api';

class UserDropDown extends React.Component {
  // Adapted from - https://reactjs.org/docs/faq-ajax.html
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      selectValue: null
    };
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
    const { error, isLoaded, items, selectValue } = this.state;
    const user_id = this.props.value ? this.props.value : '';
    const onChange = this.props.onChange;
    function callback(item) {
      if (item.id == this.user_id) {
        return <option value={item.id} selected>{item.name}</option>
      } else {
        return <option value={item.id}>{item.name}</option>
      }
    };

    const optionTemplate = items.map(callback, {
      user_id: user_id
    });

    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <label>
          Select User:
        <select name="user_id" value={this.state.selectValue} onChange={onChange}>
            <option>--select users--</option>
            {optionTemplate}
          </select>
        </label>
      );
    }
  }
}

export default UserDropDown;

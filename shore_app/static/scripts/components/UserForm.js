import React, { useState } from 'react';
import validator from 'validator'

const UserForm = (props) => {
  const [user, setUser] = useState({
    name: props.user ? props.user.name : '',
    email: props.user ? props.user.email : '',
  });
  console.log("BANG");
  console.log(props);
  const [errorMsg, setErrorMsg] = useState('');
  const { name, email } = user;

  const handleOnSubmit = (event) => {
    event.preventDefault();
    let errorMsg = '';

    if (name == '' || email == '') {
      errorMsg = 'Please fill out all the fields.';
    } else if (!validator.isEmail(email)) {
      errorMsg = 'Please enter a valid email address';
    }

    if (errorMsg == '') {
      const user = {
        name,
        email,
      };
      props.handleOnSubmit(user);
    }
    setErrorMsg(errorMsg);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setUser((prevState) => ({
      ...prevState,
      [name]: value
    }));
  };


  return (
    <div className="main-form">
      <br />
      {errorMsg && <p className="errorMsg">{errorMsg}</p>}
      <br />

      <form onSubmit={handleOnSubmit}>
        <label>
          Name:
          <input type="text" name="name" value={name} onChange={handleInputChange} />
        </label>
        <label>
          Email:
          <input type="text" name="email" value={email} onChange={handleInputChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
};

export default UserForm;

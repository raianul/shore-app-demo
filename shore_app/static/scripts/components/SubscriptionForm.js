import React, { useState } from 'react';
import UserDropDown from '../components/UserDropDown';

const SubscriptionForm = (props) => {
  console.log("proop");
  console.log(props.subscription);
  const [subscription, setSubscription] = useState({
    user_id: props.subscription ? props.subscription.user_id : '',
    interval: props.subscription ? props.subscription.interval : '',
    phrases: props.subscription ? props.subscription.phrases : '',
  });
  const [errorMsg, setErrorMsg] = useState('');
  const { user_id, interval, phrases } = subscription;

  // this.countryData = [
  //   { value: 'USA', name: 'USA' },
  //   { value: 'CANADA', name: 'CANADA' }
  // ];

  const handleOnSubmit = (event) => {
    event.preventDefault();
    let errorMsg = '';

    if (interval == '' || phrases == '') {
      errorMsg = 'Please fill out all the fields.';
    }

    if (errorMsg == '') {
      const subscription = {
        user_id,
        interval,
        phrases,
      };
      console.log("VAAA");
      console.log(subscription);
      props.handleOnSubmit(subscription);
    }
    setErrorMsg(errorMsg);
  };

  const handleInputChange = (event) => {

    const { name, value } = event.target;
    console.log(value);
    setSubscription((prevState) => ({
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

        <UserDropDown value={user_id} onChange={handleInputChange} />

        <label>
          Interval (Min):
          <input type="text" name="interval" value={interval} onChange={handleInputChange} />
        </label>
        <label>
          Phrases:
          <input type="text" name="phrases" value={phrases} onChange={handleInputChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
};


export default SubscriptionForm;

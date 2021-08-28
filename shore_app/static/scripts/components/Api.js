export default async function fetchAPI(methodType, url, data) {
  console.log(url);
  try {
    let response = await fetch(url, {
      method: methodType,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    console.log("in")
    console.log(response);
    // console.log(response.json());
    return response;
    // wait until request is done
    // let responseOK = response && response.ok;
    // if (responseOK) {
    //   let data = await response.json();
    //   // do something with data
    //   return data;
    // } else {
    //   return response;
    // }
  } catch (error) {
    return error
  }
}

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
    return response;
  } catch (error) {
    return error
  }
}

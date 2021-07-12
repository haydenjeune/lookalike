export function getImageSrc(celebName: string) {
  //  return encodeURI(
  //    "https://lookalike-manual.s3-ap-southeast-2.amazonaws.com/" +
  //      celebName +
  //      "/0.jpg"
  //  );
  return encodeURI(
    "http://localhost:5678/" + celebName.replace(/[^\w]|_/g, "") + "/main.jpeg"
  );
}

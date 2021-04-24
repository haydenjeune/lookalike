export function getImageSrc(celebName: string) {
  return encodeURI(
    "https://lookalike-manual.s3-ap-southeast-2.amazonaws.com/" +
      celebName +
      "/0.jpg"
  );
}

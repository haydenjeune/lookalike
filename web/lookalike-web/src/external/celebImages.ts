export function getImageSrc(celebName: string) {
  return encodeURI(
    "http://localhost:8081/" + celebName.replace(/[^\p{L}]/ug, "") + "/main.jpeg"
  );
}

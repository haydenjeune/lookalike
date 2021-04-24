export type CelebMatches = {
  name: string;
  similarity: number;
}[];

export async function findMatches(data: string): Promise<CelebMatches> {
  return fetch("http://localhost:5000/find", {
    method: "post",
    body: data,
    headers: {
      "Content-Type": "image/jpeg",
    },
  }).then((response) => {
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    return response.json();
  });
}

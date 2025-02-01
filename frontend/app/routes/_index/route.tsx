import type { Route } from "./+types/route";

export function meta({}: Route.MetaArgs) {
  return [{ title: "ParlerMent" }];
}

export default function Index() {
  return <p>Hello world! </p>;
}

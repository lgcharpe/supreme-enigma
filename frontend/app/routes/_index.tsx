import type { Route } from "./+types/_index";

export function meta({}: Route.MetaArgs) {
  return [{ title: "DemocracyUpdate" }];
}

export default function Index() {
  return (
    <>
      <h1></h1>
    </>
  );
}

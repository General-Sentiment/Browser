// Redirect homepage to the Following feed
if (location.pathname === "/" && !location.search.includes("variant=following")) {
  location.replace("/?variant=following");
}

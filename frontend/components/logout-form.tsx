export function LogoutForm(): JSX.Element {
  return (
    <form action="/api/auth/logout" method="post">
      <button
        className="rounded-full border border-ink/15 px-4 py-2 text-sm font-semibold text-ink transition hover:border-ink/35"
        type="submit"
      >
        Log Out
      </button>
    </form>
  );
}


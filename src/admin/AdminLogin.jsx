export default function AdminLogin() {
  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <form className="bg-white p-8 rounded-lg shadow w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Admin Login</h2>
        <input type="text" placeholder="Username" className="w-full mb-4 p-3 border rounded" />
        <input type="password" placeholder="Password" className="w-full mb-4 p-3 border rounded" />
        <button className="w-full bg-indigo-500 text-white p-3 rounded hover:bg-indigo-600">
          Login
        </button>
      </form>
    </div>
  );
}

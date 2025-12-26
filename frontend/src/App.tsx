import { AuthProvider } from "./auth/AuthProvider";
import Login from "./pages/Login";

function App() {
  return (
    <AuthProvider>
      <Login />
    </AuthProvider>
  );
}

export default App;

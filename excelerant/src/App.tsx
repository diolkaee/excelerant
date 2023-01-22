import "./App.css";
import { ExcelerantContext } from "./contexts/ExcelerantContext";
import MainPage from "./routes/MainPage";

const ws = new WebSocket(
  `ws://${import.meta.env.VITE_SERVER_URL}:${import.meta.env.VITE_SERVER_PORT}`
);

function App() {
  return (
    <ExcelerantContext.Provider value={ws}>
      <MainPage />
    </ExcelerantContext.Provider>
  );
}

export default App;

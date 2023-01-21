import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
  const appPort = process.env.VITE_APP_PORT;

  return defineConfig({
    server: {
      // Use custom port if available, else resort to default port (5173)
      port: appPort ? parseInt(appPort) : undefined,
    },
    plugins: [react(), svgr()],
  });
};

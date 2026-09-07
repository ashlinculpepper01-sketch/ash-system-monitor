const ids = {
  status: document.getElementById("status"),
  hostname: document.getElementById("hostname"),
  os: document.getElementById("os"),
  localIp: document.getElementById("localIp"),
  processCount: document.getElementById("processCount"),
  uptime: document.getElementById("uptime"),
  cpuValue: document.getElementById("cpuValue"),
  cpuBar: document.getElementById("cpuBar"),
  ramValue: document.getElementById("ramValue"),
  ramBar: document.getElementById("ramBar"),
  ramText: document.getElementById("ramText"),
  diskValue: document.getElementById("diskValue"),
  diskBar: document.getElementById("diskBar"),
  diskText: document.getElementById("diskText"),
  download: document.getElementById("download"),
  upload: document.getElementById("upload"),
  timestamp: document.getElementById("timestamp"),
  terminalLog: document.getElementById("terminalLog")
};

let previousStatus = null;

function pct(value) {
  return `${value}%`;
}

function addTerminalLine(text) {
  const p = document.createElement("p");
  p.textContent = `> ${text}`;
  ids.terminalLog.prepend(p);

  while (ids.terminalLog.children.length > 7) {
    ids.terminalLog.removeChild(ids.terminalLog.lastChild);
  }
}

async function refresh() {
  try {
    const response = await fetch("/api/stats", { cache: "no-store" });
    const data = await response.json();

    ids.status.textContent = data.status;
    ids.hostname.textContent = data.hostname;
    ids.os.textContent = data.os;
    ids.localIp.textContent = data.local_ip;
    ids.processCount.textContent = data.process_count;
    ids.uptime.textContent = data.uptime;

    ids.cpuValue.textContent = pct(data.cpu_percent);
    ids.cpuBar.style.width = pct(data.cpu_percent);

    ids.ramValue.textContent = pct(data.ram_percent);
    ids.ramBar.style.width = pct(data.ram_percent);
    ids.ramText.textContent = `${data.ram_used_gb} / ${data.ram_total_gb} GB`;

    ids.diskValue.textContent = pct(data.disk_percent);
    ids.diskBar.style.width = pct(data.disk_percent);
    ids.diskText.textContent = `${data.disk_used_gb} / ${data.disk_total_gb} GB`;

    ids.download.textContent = `${data.download_kbps} KB/s`;
    ids.upload.textContent = `${data.upload_kbps} KB/s`;
    ids.timestamp.textContent = data.timestamp;

    if (previousStatus !== data.status) {
      addTerminalLine(`system status changed: ${data.status}`);
      previousStatus = data.status;
    }

    addTerminalLine(
      `cpu ${data.cpu_percent}% | ram ${data.ram_percent}% | disk ${data.disk_percent}%`
    );
  } catch (error) {
    ids.status.textContent = "OFFLINE";
    addTerminalLine("telemetry endpoint unavailable");
  }
}

refresh();
setInterval(refresh, 2000);

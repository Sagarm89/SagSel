package org.openqa.selenium.bidi.webextension;

import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.manager.SeleniumManager;
import org.openqa.selenium.testing.JupiterTestBase;

public class WebExtensionTest extends JupiterTestBase {

  private final Map<String, String> extensionData = Map.of(
    "id", "1FC7D53C-0B0A-49E7-A8C0-47E77496A919@web-platform-tests.org",
    "path", getExtensionPath("unpacked-extension"),
    "archivePath", getExtensionPath("signed.xpi")
  );

  @BeforeEach
  void setUp() {
    Logger rootLogger = Logger.getLogger("");
    Arrays.stream(rootLogger.getHandlers())
        .forEach(
            handler -> {
              handler.setLevel(Level.FINE);
            });
    Logger smLogger = Logger.getLogger(SeleniumManager.class.getName());
    smLogger.setLevel(Level.FINE);
    FirefoxOptions options = new FirefoxOptions();
    options.setBinary("/Applications/Firefox Nightly.app/Contents/MacOS/firefox");
    options.setCapability("webSocketUrl", true);
    driver = new FirefoxDriver(options);
  }

  public static String getExtensionPath(String filename) {
    String currentDir = Paths.get("").toAbsolutePath().toString();
    return Paths.get(currentDir, "webextension", filename).toString();
  }

  @Test
  void installExtensionPath() {
    WebExtension extension = new WebExtension(driver);
    var exIn =
        extension.Install(
            new InstallExtensionParameters(
                new ExtensionPath(
                  extensionData.get("path"))));
    assert exIn.get("extension")
        .equals(extensionData.get("id"));

    extension.Uninstall(new UninstallExtensionParameters(exIn));
  }

  @Test
  void installArchiveExtensionPath() {
    WebExtension Extension = new WebExtension(driver);
    var ex =
      Extension.Install(
        new InstallExtensionParameters(
          new ExtensionArchivePath(
            extensionData.get("archivePath"))));
    assert ex.get("extension")
      .equals(extensionData.get("id"));

    Extension.Uninstall(new UninstallExtensionParameters(ex));
  }

}

package org.openqa.selenium.support;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import org.openqa.selenium.WebElement;

public final class BrokenLinkChecker {

    private BrokenLinkChecker() {
        // Utility class - prevent instantiation
    }

    public static boolean isBroken(WebElement element) {
        String url = element.getAttribute("href");
        if (url == null || url.trim().isEmpty()) {
            return false; 
        }
        return isBroken(url.trim());
    }

    public static boolean isBroken(String linkURL) {
        try {
            URL url = URI.create(linkURL).toURL();
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("HEAD");
            connection.setConnectTimeout(5000); // 5 sec timeout
            connection.setReadTimeout(5000);
            connection.connect();

            int responseCode = connection.getResponseCode();
            connection.disconnect();

            return responseCode >= 400;
        } catch (IOException e) {
            System.err.println("Error checking link: " + linkURL + " → " + e.getMessage());
            return true; 
        }
    }
}
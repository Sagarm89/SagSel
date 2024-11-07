using NUnit.Framework;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Nodes;

namespace OpenQA.Selenium.Remote
{
    [TestFixture]
    public class RemoteSessionCreationTests : DriverTestFixture
    {
        [Test]
        public void CreateChromeRemoteSession()
        {
            IWebDriver chrome = new ChromeRemoteWebDriver();
            chrome.Url = xhtmlTestPage;
            try
            {
                Assert.AreEqual("XHTML Test Page", chrome.Title);
            }
            finally
            {
                chrome.Quit();
            }
        }

        [Test]
        public void CreateFirefoxRemoteSession()
        {
            IWebDriver firefox = new FirefoxRemoteWebDriver();
            firefox.Url = xhtmlTestPage;
            try
            {
                Assert.AreEqual("XHTML Test Page", firefox.Title);
            }
            finally
            {
                firefox.Quit();
            }
        }

        [Test]
        public void CreateEdgeRemoteSession()
        {
            IWebDriver edge = new EdgeRemoteWebDriver();
            edge.Url = xhtmlTestPage;
            try
            {
                Assert.AreEqual("XHTML Test Page", edge.Title);
            }
            finally
            {
                edge.Quit();
            }
        }

        [Test]
        public void ShouldSetRemoteSessionSettingsMetadata()
        {
            var settings = new RemoteSessionSettings();

            Assert.That(settings.HasCapability("a"), Is.False);

            settings.AddMetadataSetting("a", null);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.Null);

            settings.AddMetadataSetting("a", true);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.True);

            settings.AddMetadataSetting("a", false);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.False);

            settings.AddMetadataSetting("a", 123);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.TypeOf<int>().And.EqualTo(123));

            settings.AddMetadataSetting("a", 123f);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.TypeOf<float>().And.EqualTo(123f));

            settings.AddMetadataSetting("a", 123d);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.TypeOf<double>().And.EqualTo(123d));

            JsonNode trueName = JsonValue.Create(true);
            settings.AddMetadataSetting("a", trueName);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.InstanceOf<JsonNode>().And.EqualTo(trueName).Using<JsonNode>(JsonNode.DeepEquals));

            var reader = new Utf8JsonReader("false"u8);
            JsonElement trueElement = JsonElement.ParseValue(ref reader);

            settings.AddMetadataSetting("a", trueElement);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.TypeOf<JsonElement>().And.Matches<JsonElement>(static left =>
            {
                return left.ValueKind == JsonValueKind.False;
            }));

            List<int> intValues = [1, 2, 3];
            settings.AddMetadataSetting("a", intValues);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.TypeOf<List<int>>().And.EqualTo(intValues));

            Dictionary<string, int> dictionaryValues = new Dictionary<string, int>
            {
                {"value1", 1 },
                {"value2", 1 },
            };
            settings.AddMetadataSetting("a", dictionaryValues);
            Assert.That(settings.HasCapability("a"));
            Assert.That(settings.GetCapability("a"), Is.TypeOf<Dictionary<string, int>>().And.EqualTo(dictionaryValues));
        }
    }
}

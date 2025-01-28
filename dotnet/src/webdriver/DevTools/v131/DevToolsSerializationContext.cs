using System.Text.Json.Serialization;

namespace OpenQA.Selenium.DevTools.V131;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V131RequestSerializationContext : JsonSerializerContext;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V131ResponseSerializationContext : JsonSerializerContext;

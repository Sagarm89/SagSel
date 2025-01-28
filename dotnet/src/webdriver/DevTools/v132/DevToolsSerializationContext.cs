using System.Text.Json.Serialization;

namespace OpenQA.Selenium.DevTools.V132;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V132RequestSerializationContext : JsonSerializerContext;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V132ResponseSerializationContext : JsonSerializerContext;
